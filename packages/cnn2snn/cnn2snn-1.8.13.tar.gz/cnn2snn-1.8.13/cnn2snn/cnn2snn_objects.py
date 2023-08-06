#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""CNN2SNN objects required to serialize Keras quantized models.
"""

from .quantization_ops import (StdWeightQuantizer, TrainableStdWeightQuantizer,
                               MaxQuantizer, MaxPerAxisQuantizer,
                               ScaleFactorQuantizer)
from .quantization_layers import (QuantizedConv2D, QuantizedSeparableConv2D,
                                  QuantizedDense, ActivationDiscreteRelu,
                                  QuantizedReLU)

cnn2snn_objects = {
    'StdWeightQuantizer': StdWeightQuantizer,
    'TrainableStdWeightQuantizer': TrainableStdWeightQuantizer,
    'MaxQuantizer': MaxQuantizer,
    'MaxPerAxisQuantizer': MaxPerAxisQuantizer,
    'ScaleFactorQuantizer': ScaleFactorQuantizer,
    'QuantizedConv2D': QuantizedConv2D,
    'QuantizedSeparableConv2D': QuantizedSeparableConv2D,
    'QuantizedDense': QuantizedDense,
    'ActivationDiscreteRelu': ActivationDiscreteRelu,
    'QuantizedReLU': QuantizedReLU
}
