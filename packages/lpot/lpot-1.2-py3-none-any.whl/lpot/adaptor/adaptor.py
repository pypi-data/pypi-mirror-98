#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import abstractmethod

'''The framework backends supported by lpot, including tensorflow, mxnet and pytorch.

   User could add new backend support by implementing new Adaptor subclass under this directory.
   The naming convention of new Adaptor subclass should be something like ABCAdaptor, user
   could choose this framework backend by setting "abc" string in framework field of yaml.

   FRAMEWORKS variable is used to store all implemented Adaptor subclasses of framework backends.
'''
FRAMEWORKS = {}


def adaptor_registry(cls):
    '''The class decorator used to register all Adaptor subclasses.

       Args:
           cls (class): The class of register.
    '''
    assert cls.__name__.endswith(
        'Adaptor'), "The name of subclass of Adaptor should end with \'Adaptor\' substring."
    if cls.__name__[:-len('Adaptor')].lower() in FRAMEWORKS:
        raise ValueError('Cannot have two frameworks with the same name.')
    FRAMEWORKS[cls.__name__[:-len('Adaptor')].lower()] = cls
    return cls


class Adaptor(object):
    '''The base class of framework adaptor layer.

    '''

    def __init__(self, framework_specific_info):
        pass

    @abstractmethod
    def quantize(self, tune_cfg, model, dataloader, q_func=None):
        '''The function is used to do calibration and quanitization in post-training quantization.

           Args:
               tune_cfg(dict): The chosen tuning configuration.
               model (object): The model to do calibration.
               dataloader(object): The dataloader used to load calibration dataset.
               q_func (optional): training function for quantization aware training mode.
        '''
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, model, dataloader, postprocess=None,
                 metric=None, measurer=None, iteration=-1, tensorboard=False):
        '''The function is used to run evaluation on validation dataset.

           Args:
               model (object): The model to do calibration.
               dataloader (generator): generate the data and labels.
               postprocess (object, optional): process the result from the model
               metric (object, optional): Depends on model category. Defaults to None.
               measurer (object, optional): for precise benchmark measurement.
               iteration(int, optional): control steps of mini-batch
               tensorboard (boolean, optional): for tensorboard inspect tensor.
        '''
        raise NotImplementedError

    @abstractmethod
    def query_fw_capability(self, model):
        '''The function is used to return framework tuning capability.

           Args:
               model (object): The model to query quantization tuning capability.
        '''
        raise NotImplementedError

    @abstractmethod
    def query_fused_patterns(self, model):
        '''The function is used to run fused patterns in framework.

           Args:
               model (object): The model to do calibration.

           Return:
              [['conv', 'relu'], ['conv', 'relu', 'bn']]
        '''
        raise NotImplementedError

    @abstractmethod
    def inspect_tensor(self, model, dataloader, op_list=[], iteration_list=[]):
        '''The function is used by tune strategy class for dumping tensor info.

           Args:
               model (object): The model to do calibration.
           Return:
               Numpy Array Dict
               {'op1': tensor, 'op2': tensor}
        '''
        raise NotImplementedError

    @abstractmethod
    def mapping(self, src_model, dst_model):
        '''The function is used to create a dict to map tensor name
           of src model to tensor name of dst model.

           Return:
               Dict
               {'src_op1': 'dst_op1'}
        '''
        raise NotImplementedError

    def quantize_input(self, model):
        ''' quantize the model to be able to take quantized input

            Args:
                model (object): The model to quantize input

            Return:
                model (object): The quantized input model
                scale (float): The scale for dataloader to generate quantized input
        '''
        return model, 1.

    @abstractmethod
    def _pre_eval_hook(self, model):
        '''The function is used to do some preprocession before evaluation phase.

        Return:
              model
        '''
        raise NotImplementedError

    @abstractmethod
    def _post_eval_hook(self, model, **args):
        '''The function is used to do some post process after complete evaluation.
        '''
        raise NotImplementedError

    @abstractmethod
    def save(self, model, path):
        '''The function is used by tune strategy class for saving model.

           Args:
               model (object): The model to saved.
               path (string): The path where to save.
        '''
        raise NotImplementedError
