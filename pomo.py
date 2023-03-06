# import os
import curses


def main(stdscr):

    # curses setup
    stdscr.nodelay(1)
    stdscr.timeout(1000)
    curses.curs_set(0)
    curses.use_default_colors()
    rows, cols = stdscr.getmaxyx()

    # timer and state variables
    timer = 60 * pomo_len
    state = 'pomo'
    pause = False

    while True:

        # keypresses
        key = stdscr.getch()
        if key == ord('q'):
            exit()
        elif key == ord('p'):
            if not pause:
                timer += 1
            pause = not pause
        stdscr.erase()

        hour = timer // 60
        sec_str = f'{timer - hour * 60:02d}'

        # blink text for the last 10 seconds
        if timer <= 10 and timer % 2 == 0:
            col = curses.A_REVERSE
        else:
            col = curses.color_pair(0)

        # screen output
        stdscr.addstr(0, 0, 'Pomodoro timer', col)
        stdscr.addstr(1, 0, '==============', col)
        if pause:
            stdscr.addstr(0, 15, '* PAUSED')
        if state == 'pomo':
            stdscr.addstr(3, 0, 'Task: ' + pomo_str, col)
        else:
            stdscr.addstr(3, 0, 'Have a rest.', col)
            # system notification and sound
            # if timer == break_len * 60:
            #     os.system(
            #         'notify-send -t 5000 'Pomodoro finished. ' +
            #         f'Have a {break_len} minute break''
            #     )
            #     os.system('play -q -V0 ding.mp3')
        stdscr.addstr(4, 0, f'Remaining time: {hour}:{sec_str}', col)
        stdscr.addstr(6, 0, 'q: exit p: pause', col)

        stdscr.refresh()

        # advance and check timer
        if not pause:
            timer -= 1

        if timer == -1 and state == 'pomo':
            state = 'break'
            timer = 60 * break_len
        elif timer == -1:
            break


pomodoro = 1
pomo_list = []

# parameter input
while pomodoro <= 4:
    # os.system('clear')
    if pomodoro == 1:
        pomo_str = input(f'\nEnter task #{pomodoro}: ')
        pomo_list.append(pomo_str)
        pomo_len = input('Enter pomodoro length in minutes (25): ')
        if pomo_len == '':
            pomo_len = 25
        else:
            pomo_len = int(pomo_len)
        break_len = input('Enter break length in minutes (5): ')
        if break_len == '':
            break_len = 5
        else:
            break_len = int(break_len)
    else:
        pomo_str = input(f'\nEnter task #{pomodoro} ({pomo_list[-1]}): ')
        if pomo_str == '':
            pomo_str = pomo_list[-1]
        else:
            pomo_list.append(pomo_str)

    curses.wrapper(main)

    pomodoro += 1

print('\nPomodoro session finished!\n')
print('You worked on the following tasks: ')

for item in pomo_list:
    print('- ' + item)

print('')
