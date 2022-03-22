import setuptools

version = {}
with open("../../app0-admin/config/version.py") as fp:
    exec(fp.read(), version)


def read_requirements_txt():
    with open("../../requirements.txt") as fb:
        libs = {}
        for line in fb.readlines():
            for op in (">=", "=="):
                try:
                    idx = line.index(op)
                    libs[line[0:idx]] = line[idx+2:]
                except ValueError:
                    pass
    return libs


def read_requirements_lock():
    with open("../../requirements.lock") as fb:
        libs = {}
        for line in fb.readlines():
            lv = line.split("==")
            if len(lv) > 1:
                libs[lv[0]] = lv[1].strip('\n')
    return libs


req_versions = read_requirements_txt()
locked_versions = read_requirements_lock()


def libversion(lib):
    lib_source = "../../requirements.txt"
    lib_version = req_versions.get(lib)
    if lib_version is None:
        lib_source = "requirements.lock"
        lib_version = locked_versions[lib.split('[')[0]]
    print(lib_source, f"{lib}>={lib_version}")
    return lib_version


setuptools.setup(
    name="app0.platform.auth",
    version=version['APP0_ADMIN_VERSION'],
    description="Platform Auth Plugin",
    package_dir={
        "": "src"
    },
    packages=[
        "app0.platform.auth",
    ],
    include_package_data=True,
    package_data={
        "app0.platform.auth": ["py.typed"]
    },
    python_requires=">=3.9",
    install_requires=[
        "app0.admin",
        "hopeit.engine[web,cli,fs-storage,redis-streams,apps-visualizer,config-manager,apps-client]",
        "motor"
    ].append(f"app0.admin=={version['APP0_ADMIN_VERSION']}"),
    extras_require={
    },
    entry_points={
    }
)
