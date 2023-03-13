#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 14:47
# @Author  : Tom SONG 
# @Mail    : xdmyssy@gmail.com
# @File    : ReadRoot.py
# @Software: PyCharm

import numpy as np
import uproot


class ReadRoot():

    def __init__(self, file_path):
        self.file_path = file_path
        self.root_file = uproot.open(file_path)
        tree = self.root_file['Raw_Hit']
        self.tree = tree.arrays(library='np')

    def readBranch(self, branch):
        return self.tree[branch]


def dirInit(layer):
    dict = {}
    for i in range(layer):
        dict[i] = 0
    return dict


def findMuonTrack(hit_tags, layers, trigger_ID, layer_num):
    trigger_ID_picked = []
    for i in range(layers):

        dicts = dirInit(layer_num)
        layers_fired = 0
        cells_fired = 0
        notshower = True

        hit_tags_event = hit_tags[i]
        layers_event = layers[i]

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

        if notshower and (cells_fired / layers_fired < 1.5) and (layers_fired > (0.7 * layer_num)):
            trigger_ID_picked.append(trigger_ID[i])

    return np.array(trigger_ID_picked)


if __name__ == '__main__':


    pass
