from copier import run_copy, run_update

def main():
    print("Hello from scaffolding-custom!")
    # Create a project from a local path
    # run_copy(src_path="git@github.com:noorul90/fastapi-project-skeleton.git", dst_path="fastapi-project", vcs_ref="HEAD", defaults=False,)
    run_copy(".", "fastapi-project")
    # run_update(dst_path=".", defaults=True, overwrite=True,)


if __name__ == "__main__":
    main()
