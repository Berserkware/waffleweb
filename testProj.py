from waffleweb import WaffleProject

apps = [
    'MathAPI',
]

proj = WaffleProject(apps)

if __name__ == '__main__':
    proj.run('127.0.0.1', 8080)