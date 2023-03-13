#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 19:32
# @Author  : Tom SONG 
# @Mail    : xdmyssy@gmail.com
# @File    : checkshift.py

# @Software: PyCharm

from Data.ReadRoot import findMuonTrack,ReadRoot
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os



def main(ecal_file_path,ahcal_file_path,save_dir):

    hittag = 'HitTag'
    layer = 'Layer'
    triggerid = 'TriggerID'


    ecal_root = ReadRoot(ecal_file_path)
    ahcal_root = ReadRoot(ahcal_file_path)

    ecal_hit_tag = ecal_root.readBranch(hittag)
    ecal_layer = ecal_root.readBranch(layer)
    ecal_triggerid = ecal_root.readBranch(triggerid)

    assert len(ecal_layer) == len(ecal_hit_tag)
    assert len(ecal_layer) == len(ecal_triggerid)

    ahcal_hit_tag = ahcal_root.readBranch(hittag)
    ahcal_layer = ahcal_root.readBranch(layer)
    ahcal_triggerid = ahcal_root.readBranch(triggerid)

    assert len(ahcal_layer) == len(ahcal_hit_tag)
    assert len(ahcal_layer) == len(ahcal_triggerid)

    # find muon in ecal
    ecal_triggerid_picked = findMuonTrack(hit_tags=ecal_hit_tag, layers=ecal_layer, trigger_ID=ecal_triggerid,
                                          layer_num=32)
    ahcal_triggerid_picked = findMuonTrack(hit_tags=ahcal_hit_tag, layers=ahcal_layer, trigger_ID=ahcal_triggerid,
                                           layer_num=40)

    results = []
    for e_trigid in ecal_triggerid_picked:
        for h_trigid in ahcal_triggerid_picked:
            results.append(e_trigid - h_trigid)

    shifts = np.array(results)

    max_shift = np.amax(shifts)
    min_shift = np.amin(shifts)

    fig = plt.figure(figsize=(6, 5))
    plt.hist(results, bins=(max_shift - min_shift+1), range=[min_shift-0.5, max_shift+0.5])
    fig_save_path = os.path.join(save_dir, '{}.png'.format(ecal_file_path[-27,-21]))
    plt.savefig(fig_save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # base setting

    parser.add_argument("--ecal_file_path", type=str, help="root file.")
    parser.add_argument("--ahcal_file_path", type=str, help="root file.")
    parser.add_argument("--save_dir", type=str, help="dir for save.")
    args = parser.parse_args()

    main(ecal_file_path=args.ecal_file_path,ahcal_file_path=args.ahcal_file_path,save_dir=args.save_dir)

    pass
