import oloren as olo
import sys
import io

@olo.register()
def hello():
    return "Hello World!"

if __name__ == "__main__":
    olo.run("alpha", port=80)