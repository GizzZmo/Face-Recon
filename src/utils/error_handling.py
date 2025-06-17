import traceback

def log_error(exc):
    with open("error.log", "a") as f:
        f.write(traceback.format_exc())
    print(f"Error: {exc}")

def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e)
    return wrapper
