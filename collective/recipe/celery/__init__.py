import logging
import os
import zc.buildout
import zc.recipe.egg
from options import STRING_OPTIONS, NUMERIC_OPTIONS, SEQUENCE_OPTIONS


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        options.setdefault('config-path',
                os.path.join(self.buildout['buildout']['parts-directory'],
                                 self.name))

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )

    def install(self):
        options = self.options
        logger = logging.getLogger(self.name)

        config_lines = []
        for k, v in options.items():
            if k in STRING_OPTIONS:
                config_lines.append('%s = %s' % (STRING_OPTIONS[k], repr(v)))
            elif k in NUMERIC_OPTIONS:
                config_lines.append('%s = %s' % (NUMERIC_OPTIONS[k], v))
            elif k in SEQUENCE_OPTIONS:
                config_lines.append('%s = %s' % (SEQUENCE_OPTIONS[k],
                                                 repr(tuple(v.split()))))

        if 'additional-config' in options:
            config_lines.append(options['additional-config'])

        config_lines.sort()

        conf_filename = os.path.join(options['config-path'],
                                     'celeryconfig.py')
        if not os.path.exists(os.path.dirname(conf_filename)):
            logger.info('Creating directory %s.' %
                        os.path.dirname(conf_filename))
            os.makedirs(os.path.dirname(conf_filename))

        conf_file = open(conf_filename, 'w')
        conf_file.write('\n'.join(config_lines))
        conf_file.close()
        logger.info('Generated config file %s.' % conf_filename)

        celery_egg_options = {
            'eggs': 'celery',
            'extra-paths': os.path.dirname(conf_filename)}
        if 'eggs' in options:
            celery_egg_options['eggs'] = '\n'.join(['celery']
                                         + options['eggs'].split())
        if 'scripts' in options:
            celery_egg_options['scripts'] = options['scripts']
        celery_egg = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            celery_egg_options,
        )

        return [conf_filename] + list(celery_egg.install())

    def update(self):
        pass
