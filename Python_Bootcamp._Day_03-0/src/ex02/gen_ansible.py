import yaml

# Initialization
with open('../../materials/todo.yml', 'r') as f:
    data = yaml.safe_load(f)
tasks = []
result = []

# Bad guys and script
bad_guys = data['bad_guys']
run_flags_args = '"python exploit.py && python consumer.py -e 4815162342,3133780085"'

# Packages
packages = data['server']['install_packages']
pip_packages = ['redis', 'json', 'beautifulsoup4']

# Packages playbook
install_apt_packages = []
install_pip_packages = []
for package in packages:
    install_apt_packages.append({'name': 'Install ' + package, 'apt': ['name=' + package, 'state=latest']})
install_pip_packages.append({'name': 'Install pip_packages', 'pip': {'name': pip_packages}})
install_packages = install_apt_packages + install_pip_packages

# Copy scripts playbook
copy_scripts = []
scripts = ['/exploit.py', '/consumer.py']
for script in scripts:
    copy_scripts.append({'name': 'Copy ' + script, 'ansible.builtin.copy': {'src': script, 'dest': script}})

# Run scripts playbook
run_scripts = []
run_scripts.append({'name': 'Run scripts', 'raw': run_flags_args})

# Result file
tasks = install_packages + copy_scripts + run_scripts
init = {'hosts': 'server', 'tasks': tasks}
result.append(init)

# Final
with open('deploy.yml', 'w') as f:
    f.write(yaml.dump(result, sort_keys=False))
