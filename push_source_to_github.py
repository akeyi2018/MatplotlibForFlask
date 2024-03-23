import os
from datetime import datetime
import subprocess as cmd

class push_git:

    @staticmethod
    def shell_cmd(content):
        try:
            # カレントディレクトリに移動する
            # cp1 = cmd.run(f'cd /d/python_pgm/MatplotlibForFlask')
            cp1 = cmd.run(f'git add .', shell=True)
            # cp1 = cmd.run(f'ls -la', shell=True)
            cp2 = cmd.run(f'git status', shell=True)
            if cp2.returncode == 0:
                cp3 = cmd.run(f'git commit -m {content}', shell=True)
                cp4 = cmd.run(f'git push')
                print('push Success')
            else:
                print('NG')

        except:
            print('Push Error')


if __name__ == '__main__':
    p = push_git()

    p.shell_cmd('自動Pushテスト')
