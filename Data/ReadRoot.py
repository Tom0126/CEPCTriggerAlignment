#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 14:47
# @Author  : Tom SONG 
# @Mail    : xdmyssy@gmail.com
# @File    : ReadRoot.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import numpy as np
import uproot


class ReadRoot():

    def __init__(self, file_path, tree_name):
        self.file_path = file_path
        self.root_file = uproot.open(file_path)
        tree = self.root_file[tree_name]
        self.tree = tree.arrays(library='np')

    def readBranch(self, branch):
        return self.tree[branch]


def decodeCellIDs(cellIDs):
    scale = 100000
    layers = cellIDs // scale
    # chips = (cellIDs - scale * layers) // 10000
    # memo_ids = (cellIDs - scale * layers - 10000 * chips) // 100
    # channels = cellIDs % 100
    return layers


def dirInit(layer):
    dict = {}
    for i in range(layer):
        dict[i] = 0
    return dict


def cutLoop(triggerID):
    results = [triggerID[0]]
    period = 0
    loop = 2 ** 16
    length = len(triggerID)
    i = 1
    while i < length:
        tid_current = period * loop + triggerID[i]
        tid_former = results[i - 1]
        if tid_current < tid_former:
            period += 1
        results.append(period * loop + triggerID[i])
        i += 1

    return np.array(results)


def findMuonTrack(hit_tags, cellIDs, triggerIDs, layer_num):
    trigger_ID_picked = []
    layers = decodeCellIDs(cellIDs)

    for i, cellID in enumerate(cellIDs):

        dicts = dirInit(layer_num)
        layers_fired = 0
        cells_fired = 0
        notshower = True

        layers_event = layers[i]

        if hit_tags == None:
            hit_tags_event = np.ones(len(layers_event))
        else:
            hit_tags_event = hit_tags[i]
            assert len(hit_tags_event) == len(layers_event)

        # select cells in one event
        for j, hit_tag in enumerate(hit_tags_event):
            if hit_tag:

                layer = layers_event[j]
                dicts[layer] = dicts.get(layer) + 1
                if dicts.get(layer) > 5:
                    break
            else:
                pass

        for value in dicts.values():

            if value > 5:
                notshower = False
                break

            if value:
                layers_fired += 1
                cells_fired += value

        if notshower and (cells_fired / layers_fired < 1.2) and (layers_fired > (0.8 * layer_num)):
            trigger_ID_picked.append(triggerIDs[i])

    return np.array(trigger_ID_picked)


if __name__ == '__main__':
    ecal_path = '/lustre/collider/songsiyuan/CEPC/Syn/ustc_root_file/ECAL_Run250_20221029_062916.root'
    ecal_root = uproot.open(ecal_path)
    keys = ecal_root.keys()
    print(keys)
    # triggerid=ahcal_root.readBranch('TriggerID')
    #
    # triggerid=cutLoop(triggerid)
    #
    # layers=ahcal_root.readBranch('Layer')
    # tag=ahcal_root.readBranch('HitTag')
    # picked=findMuonTrack(tag,layers,triggerid,32)
    # plt.plot(triggerid)
    # plt.plot(picked,'.')
    # plt.show()
    # print(picked)
    # print(len(picked))
    pass
