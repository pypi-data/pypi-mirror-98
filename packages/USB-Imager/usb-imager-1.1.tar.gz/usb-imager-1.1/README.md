# USB-Imager

[USB-Imager] is a GUI tool to write bootable disk images to USB key.

|[License]   | GPLv3
|--------    | --------
|*Copyright* | **&copy; 2021 by Skynet-Research**
- - - - - - -

![Screenshot]


## 1. Features

- [x] No root privileges required.
- [x] Drives get unmounted and locked (if encrypted) before writing.
- [x] Writing support for hybrid ISOs by checking the MBR signature.
- [x] Adjustable write buffer

Planned:

- [ ] Automatic deactivation of LVM2 volumes before writing
- [ ] Write to multiple USB keys simultaneously
- [ ] Checksum verification after copying
- [ ] Multilanguage support



## 2. Requirements

Requirements for an installation with `pip`:

- _Debian based linux (e.g. Ubuntu):_

    For \*ubuntu linux open `Software & Updates` and activate the `universe` repository or activate it via terminal.

    ```bash
    $ sudo add-apt-repository universe && sudo apt update
    $ sudo apt install python3-pip gir1.2-udisks-2.0 qt5-default
    ```

- _Red Hat based linux (e.g. Fedora):_

    ```bash
    $ sudo dnf install python3-pyside2
    ```

- _Slackware based linux (e.g. openSUSE):_

    ```bash
    $ sudo zypper install python3-pyside2 typelib-1_0-UDisks-2_0
    ```


## 3. Installation

- **Arch based linux:**

    The installation of `usb-imager-git` can be done via any package manager that supports the `AUR`.

    ```bash
    $ sudo pacman -S trizen
    $ trizen -S usb-imager-git
    ```

- **pip / pipenv:**

    If the distribution's own package manager is not supported yet, the USB-Imager can alternatively be installed via the Python package manager `pip`.

    Please try to install USB-Imager without **`sudo`** first. Only sometimes it necessary to do a system-wide installation, because in some distributions the search path `$PATH` is not configured correctly to find the startup program.

    ```bash
    $ pip3 install -U usb-imager
    $ pip3 uninstall usb-imager
    ```

    or [pipenv]:

    ```bash
    $ pipenv install usb-imager
    $ pipenv run usb-imager
    $ pipenv uninstall usb-imager
    ```



## 4. Usage

Start USB-Imager via the desktop icon or just type `usb-imager` in your terminal window.


## 5. Tested linux distributions

- _Arch based:_
    + Manjaro 20.2.1 "Nibia" -> `KDE Plasma`, `Xfce`, `Gnome`, `Cinnamon`, `Mate`

- _Debian based:_
    + Ubuntu "Bionic Beaver", "Focal Fossa" -> `Kylin`, `Kubuntu`, `Xubuntu`

- _Red Hat based:_
    + Fedora 33 -> `Workstation`

- _Slackware based:_
    + openSUSE 15.2 "Leap" -> `Gnome`


## 6. Support

If you want to report a bug or request a feature, you can do so [here].
You can also write an email to <skynet-devel@mailbox.org>.


## 7. Acknowledgements

Thanks to:

- the programmers at [SUSE Linux Products GmbH] for their [SUSE Studio Imagewriter].
It was the inspiration for this little tool.
- Rico for Beta-Testing.
- my loved ones for their almost infinite patience.



[USB-Imager]: https://pypi.org/project/usb-imager/
[License]: https://www.gnu.org/licenses/gpl-3.0-standalone.html
[Screenshot]: https://gitlab.com/skynet-devel/usb-imager/-/raw/master/Screenshot.webp

[pipenv]: https://pypi.org/project/pipenv/
[here]: https://gitlab.com/skynet-devel/usb-imager/issues

[SUSE Linux Products GmbH]: https://www.suse.com/
[SUSE Studio Imagewriter]: https://github.com/openSUSE/imagewriter
