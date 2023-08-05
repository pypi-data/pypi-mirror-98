import argparse
from avsim2D import avsim2D

def main():

    parser = argparse.ArgumentParser(description='Autonomous Vehicle Simulator 2D with CAN Drive-By-Wire\nAuthor : Raphaël LEBER')

    parser.add_argument('--no-CAN', dest='opt_no_CAN', default=False, help='no need to load a CAN bus')
    #parser.add_argument('--CANbus', dest='opt_CANbus', default='vcan0', help='connect to vcan0 (default), vcan1, can0, ...')
    parser.add_argument('--refresh', dest='opt_refresh', default=0, help='divide the screen refreshment frequency by your argument')

    args = parser.parse_args()

    avs = avsim2D.AvSim2D( args.opt_no_CAN, args.opt_refresh )
    avs.update()


if __name__ == "__main__":
    main()