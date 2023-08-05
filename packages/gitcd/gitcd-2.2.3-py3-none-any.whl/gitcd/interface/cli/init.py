import os

from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Init(BaseCommand):

    def run(self, branch: Branch):
        self.config.setMaster(
            self.interface.askFor(
                "Branch name for production releases?",
                False,
                self.config.getMaster()
            )
        )

        featureDefault = self.config.getFeature()
        if featureDefault is None:
            featureDefault = '<none>'
        self.config.setFeature(
            self.interface.askFor(
                "Branch name for feature development?",
                False,
                featureDefault
            )
        )

        testDefault = self.config.getTest()
        if testDefault is None:
            testDefault = '<none>'
        self.config.setTest(
            self.interface.askFor(
                "Branch name for test releases?",
                False,
                testDefault
            )
        )

        tagDefault = self.config.getTag()
        if tagDefault is None:
            tagDefault = '<none>'
        self.config.setTag(
            self.interface.askFor(
                "Version tag prefix?",
                False,
                tagDefault
            )
        )

        # ask for version type, manual or date
        versionType = self.interface.askFor(
            "Version type? You can either set your tag number" +
            " manually, read it from a version file or generate it by date.",
            ['manual', 'date', 'file'],
            self.config.getVersionType()
        )
        self.config.setVersionType(versionType)

        # if type is date ask for scheme
        if versionType == 'date':
            versionScheme = self.interface.askFor(
                "Scheme for your date-tag?" +
                " Year: %Y / Month: %m  / Day: %d /" +
                " Hour: %H / Minute: %M / Second: %S",
                '%Y.%m.%d%H%M',
                self.config.getVersionScheme()
            )
        elif versionType == 'file':
            versionScheme = self.interface.askFor(
                "From what file do you want to load your version?",
                False,
                self.config.getVersionScheme()
            )
            if not os.path.isfile(versionScheme):
                self.interface.error(
                    'Could not find your version file, ' +
                    'stick back to manual tag number!'
                )
                versionScheme = None
                versionType = 'manual'
        else:
            # you'll be asked for it while a release
            versionScheme = None

        extraReleaseCommandDefault = self.config.getExtraReleaseCommand()
        if extraReleaseCommandDefault is None:
            extraReleaseCommandDefault = '<none>'
        self.config.setExtraReleaseCommand(
            self.interface.askFor(
                "Do you want to execute some additional " +
                "commands after a release?",
                False,
                extraReleaseCommandDefault
            )
        )

        preReleaseCommandDefault = self.config.getPreReleaseCommand()
        if preReleaseCommandDefault is None:
            preReleaseCommandDefault = '<none>'
        self.config.setPreReleaseCommand(
            self.interface.askFor(
                "Do you want to execute some additional " +
                "commands before a release?",
                False,
                preReleaseCommandDefault
            )
        )

        # pass version scheme to config
        self.config.setVersionScheme(versionScheme)

        self.config.write()
