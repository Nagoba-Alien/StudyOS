from app.drive.drive import build_drive_tree, print_tree


def main():

    print("=" * 60)
    print("StudyOS")
    print("=" * 60)

    try:

        library = build_drive_tree()

        print_tree(library)

    except FileNotFoundError as e:

        print(f"\nError: {e}")

    except Exception as e:

        print(f"\nUnexpected error:\n{e}")


if __name__ == "__main__":
    main()
