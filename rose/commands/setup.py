from __future__ import unicode_literals
import datetime
import glob
import os

import pystache

from rose.base import BaseCommand
from rose.exceptions import TemplateNotFoundError


class CreateSetup(BaseCommand):
    def help(self, *args, **kwargs):
        return '\n'.join([
            "Usage: rose setup",
            "",
            "Runs a wizard to help create a `setup.py` file for your project."
        ])

    def prompt(self, msg, options=None, default=None):
        if options:
            msg = "%s [%s]" % (msg, options)

        try:
            value = raw_input(msg)

            if not value:
                return default

            return value
        except EOFError:
            return default

    def prompt_yes(self, msg, default='Y'):
        if default.upper() == 'Y':
            options = 'n/Y'
        else:
            options = 'N/y'

        yn = self.prompt(msg, options, default)
        return yn.lower() == 'y'

    def load_template(self, template_path):
        if not template_path:
            setup_path = os.path.join(os.path.dirname(__file__), '..', 'templates', template_path)

        if not os.path.exists(template_path):
            raise TemplateNotFoundError("No template at '%s'." % template_path)

        with open(template_path, 'r') as template_file:
            return template_file.read()

    def load_setup_template(self):
        setup_path = self.rose.get_config('setup_template_path')
        return self.load_template('setup_template.txt')

    def load_readme_template(self):
        setup_path = self.rose.get_config('readme_template_path')
        return self.load_template('README.rst')

    def check_setup_exists(self, new_setup_path):
        if os.path.exists(new_setup_path):
            answer = self.prompt("WARNING: 'setup.py' already exists. Overwrite?", default='N').lower()

            if not answer.startswith('y'):
                return True

        return False

    def write_setup(self, new_setup_path, setup_kwargs):
        setup_template = self.load_setup_template()
        rendered = pystache.render(setup_template, setup_kwargs)

        with open(new_setup_path, 'w') as setup_file:
            setup_file.write(rendered)

        self.exit_code = 0
        return True

    def write_readme(self, new_readme_path, setup_kwargs):
        readme_template = self.load_readme_template()
        rendered = pystache.render(readme_template, setup_kwargs)

        with open(new_readme_path, 'w') as readme_file:
            readme_file.write(rendered)

        self.exit_code = 0
        return True

    def run(self, *args, **kwargs):
        new_setup_path = os.path.join(self.rose.base_dir, 'setup.py')

        if self.check_setup_exists(new_setup_path):
            self.out('Aborting.')
            self.exit_code = 1
            return False

        setup_kwargs = self.run_wizard(*args, **kwargs)
        self.write_setup(new_setup_path, setup_kwargs)

        if setup_kwargs.get('create_readme'):
            self.write_setup(new_setup_path, setup_kwargs)

    def available_licenses(self):
        known_license_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'licenses', '*.txt')
        known_licenses = []

        for klp in glob.glob(known_license_path):
            license_name, ext = os.path.splitext(os.path.basename(klp))
            known_licenses.append(license_name)

        return known_licenses

    def create_readme(self):
        readme_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'README.rst')
        rendered = pystache.render(readme_path, setup_kwargs)

        with open(new_setup_path, 'w') as setup_file:
            setup_file.write(rendered)

        self.exit_code = 0
        return True

    def get_package_name(self):
        return self.prompt("Package Name?")

    def get_author_name(self):
        return self.prompt("Author Name?")

    def get_author_email(self):
        return self.prompt("Author Email?")

    def get_readme_path(self):
        has_readme = self.prompt_yes("Do you have a README?")

        if not has_readme:
            return ''

        return self.prompt("**Relative** path to README?")

    def get_project_url(self):
        return self.prompt("Project URL?")

    def get_license(self):
        return self.prompt("License?")

    def get_py_modules(self, package_name):
        py_modules = [
            package_name
        ]

        # Go up to ten levels deep.
        # If your package nests deeper than this, you're on your own.
        for level in range(10):
            many_globs = str('*/' * level)[:-1]
            possible_paths = os.path.join(self.rose.base_dir, package_name, many_globs, '__init__.py')

            for possible in glob.glob(possible_paths):
                module = os.path.dirname(possible)[len(self.rose.base_dir) + 1:]
                py_modules.append(module.replace(os.path.sep, '.'))

        return py_modules

    def get_dependencies(self):
        deps = []
        prompt_text = "Do you have any dependencies?"
        prompt_count = 0

        while True:
            if prompt_count > 0:
                prompt_text = "Do you have any more dependencies?"

            if not self.prompt_yes(prompt_text, default='N'):
                break

            deps.append(self.prompt('Dependency name?'))

        return deps

    def run_wizard(self, *args, **kwargs):
        setup_kwargs = {
            'package_name': self.get_package_name(),
            'full_version': self.get_version(),
            'short_description': self.get_short_description(),
            # Someone will eventually get mad about this, but I doubt new
            # users will understand it, so don't prompt for now.
            'zip_safe': 'False',
            'year': datetime.date.today().year,
        }

        author_name = self.get_author_name()
        author_email = self.get_author_email()

        if author_name or author_email:
            setup_kwargs['author'] = {}

            if author_name:
                setup_kwargs['author']['name'] = author_name

            if author_email:
                setup_kwargs['author']['email'] = author_email

        readme_path = self.get_readme_path()
        setup_kwargs['create_readme'] = False

        if not readme_path:
            setup_kwargs['create_readme'] = self.prompt_yes("Would you like me to create one for you?")

        if readme_path:
            setup_kwargs['readme'] = {
                'path': readme_path,
            }

        project_url = self.get_project_url()

        if project_url:
            setup_kwargs['has_url'] = {
                'project_url': project_url,
            }

        license = self.get_license()
        known_licenses = self.available_licenses()
        setup_kwargs['create_license'] = False

        if license in known_licenses:
            setup_kwargs['create_license'] = self.prompt_yes("Would you like me to create one for you?")

        if license:
            setup_kwargs['license'] = {
                'name': license,
            }

        # FIXME: Continue here.
        to_implement = {
            'has_py_modules': {
                'py_modules': [
                    '',
                ],
            },
            'has_packages': {
                'packages': [
                    '',
                ],
            },
            'has_package_data': {
                'module': {
                    'name': '',
                    'paths': [],
                }
            },
            'has_dependencies': {
                'requires': [],
                'install_requires': []
            },
            'has_scripts': {
                'scripts': [],
            },
            'has_classifiers': {
                'classifiers': [],
            },

        }

        return setup_kwargs


command_class = CreateSetup
