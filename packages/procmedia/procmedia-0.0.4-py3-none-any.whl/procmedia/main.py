import sys
from src.procmedia.detect import Detector
from src.procmedia import help

if __name__ == '__main__':
    command = sys.argv[1]

    if command == 'detect':
        try:
            obj = Detector(sys.argv[2], sys.argv[3], sys.argv[4])
        except Exception:
            obj = Detector(sys.argv[2], sys.argv[3])
        obj.detect()
    elif command == 'generate-haar':
        pass
    elif command == 'help':
        help.show_help()
    else:
        print("Command unknown. Check detect-cli help for more information")