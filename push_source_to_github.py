import subprocess as cmd

class push_git:

    @staticmethod
    def shell_cmd(id, content):
        num_id = str(id).zfill(10) + ':'
        try:
            cp1 = cmd.run(f'git add .', shell=True)
            # cp1 = cmd.run(f'ls -la', shell=True)
            cp2 = cmd.run(f'git status', shell=True)
            if cp2.returncode == 0:
                cp3 = cmd.run(f'git commit -m {num_id}{content}', shell=True)
                cp4 = cmd.run(f'git push')
                print('push Success')
            else:
                print('NG')
        except:
            print('Push Error')


if __name__ == '__main__':
    p = push_git()
    p.shell_cmd(1,'自動PushテストIDを追加')
