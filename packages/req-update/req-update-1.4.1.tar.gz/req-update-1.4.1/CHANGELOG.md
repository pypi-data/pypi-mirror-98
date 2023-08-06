CHANGELOG
=========

1.4.1 (2021-03-16)
------------------

 - Clean up error messages
 - Update dependencies
 - Build optimizations


1.4.0 (2021-02-21)
------------------

 - Add a new `--push` option to git push each commit to the default remote
 - Switch CI platform from CirlcCI to Drone
 - Update dependencies


1.3.4 (2021-01-18)
------------------

 - Show a warning when a dependency update changes major versions
 - Support python 3.9


1.3.3 (2020-12-25)
------------------

 - Ignore untracked files when checking repository cleanliness


1.3.2 (2020-12-05)
------------------

 - Correctly with with packages with dashes and/or underscores in name
 - Fix bug with no-op version updates


1.3.1 (2020-11-12)
------------------

 - Fix logic for chcking if the dep-update branch already exists


1.3.0 (2020-11-08)
------------------

 - Align comments on dependency lines when updating
 - Rollback dep-update branch if no dependencies were updated
 - Require that dependencies in requirements.txt files start at beginning of line
 - Cleanup


1.2.0 (2020-11-04)
------------------

 - Allow req-update to reusing an existing dep-update branch
 - Check pip version on startup and error when version is not high enough
 - Various fixes


1.1.0 (2020-10-25)
------------------

 - Make dryrun mode work correctly
 - Make verbose mode spit out all commands
 - Make CLI packaging work correctly


1.0.0 (2020-10-10)
------------------

 - Initial working release


0.0.1 (2020-10-01)
------------------
 - Initialize repository
 - PyPI placeholder
