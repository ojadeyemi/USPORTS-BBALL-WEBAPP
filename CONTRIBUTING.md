
## How to Contribute

To contribute to the USPORTS BASKETBALL WEB APP, follow these steps:

- Fork the repository to your GitHub account.
- Clone the forked repository to your local machine:

```bash
git clone https://github.com/ojadeyemi/USPORTS_WEBAPP.git

git checkout -b new-feature-or-fix #create new branch to add feature
```

### Create a virtual environment in the terminal

To create a virtual environment manually, use the following command (where ".virtualenv" is the name of the environment folder):

```bash
# macOS/Linux
# You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
python3 -m venv .virtualenv

# Windows
# You can also use `py -3 -m venv .virtualenv`
python -m venv .virtualenv
```
Double check that your python Interpreter path is in your virtual environment directory

>**Note**: To learn more about the `venv` module, read [it here](https://docs.python.org/3/library/venv.html) on Python.org.

Install dependacies with pip:

```
$ pip install -r requirements.txt
```
- Make your changes and improvements to the codebase.

- Test your changes locally to ensure they work as expected.

- Commit your changes with a descriptive commit message:


```bash

git add .
git commit -m "Add new feature"
```

Push your changes to your forked repository:

```bash
git push origin feature/new-feature
```
Open a pull request (PR) from your forked repository to the main repository.

- Provide a clear and descriptive title for your PR.
- Describe the changes you've made and why they're valuable.
- Reference any relevant issues or pull requests.
- Wait for feedback and be ready to make any necessary changes requested by the maintainers.

Once your PR is approved, your changes will be merged into the main repository.

## Code Style
Please follow the existing code style and conventions used in the project. Consistent coding style makes the codebase easier to maintain and understand for everyone.

## Reporting Issues
If you encounter any bugs, issues, or have suggestions for improvements, please open an issue on the GitHub repository. Provide as much detail as possible, including steps to reproduce the issue if applicable.

## License
By contributing to the USPORTS BASKETBALL WEB APP, you agree that your contributions will be licensed under the MIT License. See the LICENSE file for details.

Thank you for contributing and helping make it even better!
