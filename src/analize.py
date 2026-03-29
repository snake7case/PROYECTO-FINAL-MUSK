try:
    from .analyze import generate_report, main, save_report
except ImportError:
    from analyze import generate_report, main, save_report


__all__ = ["generate_report", "save_report", "main"]


if __name__ == "__main__":
    main()
