JAVA_IGNORE_PATTERNS = [
    # Java
    'hs_prr_eid*', 'replay_eid*',
    # Maven
    'target', 'pom.xml.*', 'release.properties', 'buildNumber.properties', 'dependency-reduced-pom.xml', '.mvn',
    # Gradle
    'bin', 'build', '.gradle', '.gradletasknamecache', 'gradle-app.setting', 'gradle/wrapper', 'gradle',
    # Eclipse
    '.settings', 'bin', 'tmp', '.metadata', '.classpath', '.project', '*.tmp', '*.bak', '*.swp', '*~.nib',
    'local.properties', '.loadpath', 'factorypath',
    # NetBeans
    'nbproject/private', 'nbbuild/', 'nbdist/', 'nbactions.xml', 'nb-configuration.xml',
]
