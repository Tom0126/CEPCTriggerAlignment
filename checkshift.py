#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 19:32
# @Author  : Tom SONG 
# @Mail    : xdmyssy@gmail.com
# @File    : checkshift.py

# @Software: PyCharm

from Data.ReadRoot import findMuonTrack,ReadRoot, cutLoop
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from collections import Counter



def main(ecal_file_path,ahcal_file_path,save_dir):

    hittag = 'HitTag'
    layer = 'Layer'
    triggerid = 'TriggerID'
    cellid='CellID'
    event_num='Event_Num'


    ecal_root = ReadRoot(ecal_file_path, tree_name='Raw_Hit')
    ahcal_root = ReadRoot(ahcal_file_path, tree_name='Calib_Hit')

    ecal_hit_tag = ecal_root.readBranch(hittag)
    ecal_cellIDs = ecal_root.readBranch(cellid)
    e_raw = ecal_root.readBranch(triggerid)
    ecal_triggerid=cutLoop(e_raw)


    assert len(ecal_cellIDs) == len(ecal_hit_tag)
    assert len(ecal_cellIDs) == len(ecal_triggerid)

    ahcal_hit_tag = None
    ahcal_cellIDs = ahcal_root.readBranch(cellid)
    a_raw = ahcal_root.readBranch(event_num)
    ahcal_triggerid=cutLoop(a_raw)


    assert len(ahcal_cellIDs) == len(ahcal_triggerid)

    # find muon in ecal
    ecal_triggerid_picked = findMuonTrack(hit_tags=ecal_hit_tag, cellIDs=ecal_cellIDs, triggerIDs=ecal_triggerid,
                                          layer_num=32)
    ahcal_triggerid_picked = findMuonTrack(hit_tags=ahcal_hit_tag, cellIDs=ahcal_cellIDs, triggerIDs=ahcal_triggerid,
                                           layer_num=40)

    # Fran
    results = []
    for e_trigid in ecal_triggerid_picked:
        for h_trigid in ahcal_triggerid_picked:
            results.append(e_trigid - h_trigid)

    shifts = np.array(results)
    np.save('/cefs/higgs/siyuansong/Syn/shifts.npy',shifts)
    shifts=Counter(shifts)

    filename = open(os.path.join(save_dir, '{}.txt'.format(ecal_file_path[-27:-21])), 'w')  # dict to txt
    for k, v in shifts.items():
        filename.write(str(k) + ':' + str(v))
        filename.write('\n')
    filename.close()

    fig1 = plt.figure(figsize=(6, 5))
    plt.plot(shifts.keys(),shifts.values(),'.')
    fig_save_path = os.path.join(save_dir, '{}.png'.format(ecal_file_path[-27:-21]))
    plt.savefig(fig_save_path)
    plt.close(fig1)

    fig2 = plt.figure(figsize=(6, 5))
    plt.plot(np.arange(len(e_raw)),e_raw,'.',label='ecal')
    plt.plot(np.arange(len(a_raw)),a_raw,'.',label='ahcal')
    plt.legend()
    fig_save_path = os.path.join(save_dir, 'triggerid{}.png'.format(ecal_file_path[-27:-21]))
    plt.savefig(fig_save_path)
    plt.close(fig2)

    print(e_raw)
    print(a_raw)
    # Tom
    cor = []
    for gap in np.arange(-100,101):

        ahcal_triggerid_picked = ahcal_triggerid_picked+gap

        cor.append(len(np.intersect1d(ecal_triggerid_picked,ahcal_triggerid_picked)))
    fig3 = plt.figure(figsize=(6, 5))
    plt.plot(np.arange(-100,101),cor,'.')
    fig_save_path = os.path.join(save_dir, 'cor_{}.png'.format(ecal_file_path[-27:-21]))
    plt.savefig(fig_save_path)
    plt.close(fig3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # base setting

    parser.add_argument("--ecal_file_path", type=str, help="root file.")
    parser.add_argument("--ahcal_file_path", type=str, help="root file.")
    parser.add_argument("--save_dir", type=str, help="dir for save.")
    args = parser.parse_args()

    main(ecal_file_path=args.ecal_file_path,ahcal_file_path=args.ahcal_file_path,save_dir=args.save_dir)

    pass
