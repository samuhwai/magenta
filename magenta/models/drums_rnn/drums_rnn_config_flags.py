# Copyright 2016 Google Inc. All Rights Reserved.
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
"""Provides a class, defaults, and utils for Drums RNN model configuration."""

# internal imports
import tensorflow as tf

from magenta.models.drums_rnn import drums_rnn_model

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string(
    'config',
    'drum_kit',
    "Which config to use. Must be one of 'one_drum' or 'drum_kit'.")
tf.app.flags.DEFINE_string(
    'generator_id',
    None,
    'A unique ID for the generator. Overrides the default if `--config` is '
    'also supplied.')
tf.app.flags.DEFINE_string(
    'generator_description',
    None,
    'A description of the generator. Overrides the default if `--config` is '
    'also supplied.')
tf.app.flags.DEFINE_string(
    'hparams', '{}',
    'String representation of a Python dictionary containing hyperparameter '
    'to value mapping. This mapping is merged with the default '
    'hyperparameters if `--config` is also supplied.')


class DrumsRnnConfigFlagsException(Exception):
  pass


def config_from_flags():
  """Parses flags and returns the appropriate DrumsRnnConfig.

  Returns:
    The appropriate DrumsRnnConfig based on the supplied flags.

  Raises:
     DrumsRnnConfigFlagsException: When an invalid config is supplied.
  """
  if FLAGS.config not in drums_rnn_model.default_configs:
    raise DrumsRnnConfigFlagsException(
        '`--config` must be one of %s. Got %s.' % (
            drums_rnn_model.default_configs.keys(), FLAGS.config))
  config = drums_rnn_model.default_configs[FLAGS.config]
  config.hparams.parse(FLAGS.hparams)
  if FLAGS.generator_id is not None:
    config.details.id = FLAGS.generator_id
  if FLAGS.generator_description is not None:
    config.details.description = FLAGS.generator_description
  return config