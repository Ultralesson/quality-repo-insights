IGNORE_PATTERNS = [
    # Git
    ".git",
    # Intellij
    'out', '.idea', '.idea_modules', '*.iml', '*.ipr', '*.iws',
    # vscode
    '.vscode', '.code-workspace',
    # OSX
    '.DS_Store',
    # Misc
    '*.log', '*.lock',

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
    # All System generated files
    '.*',

    # Typescript/ Javascript
    'lib-cov', 'pids', 'logs', 'results', 'tmp', 'coverage', 'dist', 'node_modules',

    # Python
    '.venv', '__pycache__', 'develop-eggs', 'var', '*.txt', '*.pit', 'sdist', 'parts', '__init__.py'
]
