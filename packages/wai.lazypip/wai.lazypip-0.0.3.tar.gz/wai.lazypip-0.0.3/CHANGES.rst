Changelog
=========

0.0.3 (2021-03-17)
------------------

- switched from using `pip.main` to launching external process via `python -m pip` as it is the
  recommended way of calling pip (see https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program)


0.0.2 (2020-09-04)
------------------

- the `install_packages` method now backs up the root logger before calling `pip.main`
  and restores it afterwards again


0.0.1 (2020-07-29)
------------------

- initial release
