import sys, requests, os, time

from deploy_util import send_discord_notification, check_health


def exec_cmd(cmd: str):
    print(cmd)
    return os.system(cmd)


GREEN_PORT = 8000
BLUE_PORT = 8001

current_flag: str | None = None
BASE_URL = "https://mandalart.ugsm.co.kr"
send_discord_notification("서버 업데이트 중...")

try:
    current_flag = check_health(BASE_URL)
except Exception as e:
    print(e)
    current_flag = "GREEN"

if not current_flag:
    raise BaseException("Flag is not specified")

deployment_port = None
if current_flag.upper() == "GREEN":
    deployment_flag = "BLUE"
    deployment_port = BLUE_PORT
    current_port = GREEN_PORT
    current_yml = "docker-compose-green.yml"
    deployment_yml = "docker-compose-blue.yml"
else:
    deployment_flag = "GREEN"
    deployment_port = GREEN_PORT
    current_port = BLUE_PORT
    current_yml = "docker-compose-blue.yml"
    deployment_yml = "docker-compose-green.yml"

print("Running docker compose up")
result = exec_cmd(f"docker compose -p {deployment_flag.lower()} -f {deployment_yml} up -d --force-recreate --build")

if result < 0:
    raise Exception(f"docker compose up failed. flag: {deployment_flag}")

is_container_run = False
print("Checking new container running...")
for i in range(0, 30):
    try:
        LOCAL_URL = "http://localhost"
        running_flag = check_health(LOCAL_URL, deployment_port)
        if running_flag.upper() == deployment_flag:
            is_container_run = True
            break
    except Exception as e:
        print(e)
    finally:
        time.sleep(5)

if not is_container_run:
    raise Exception(f"docker compose up failed. flag: {deployment_flag}")

exec_cmd(
    f"sudo sed -i 's/:{current_port}/:{deployment_port}/' /var/lib/docker/volumes/nginx-container_settings/_data/nginx.conf"
)
if exec_cmd("docker exec nginx-eggtart nginx -t"):
    raise Exception(f"failed to reload docker exec nginx-eggtart nginx -t")
exec_cmd("docker exec nginx-eggtart nginx -s reload")
is_deployed = False
for i in range(0, 15):
    try:
        running_flag = check_health(BASE_URL)
        if running_flag.upper() == deployment_flag:
            is_deployed = True
            break
    except Exception as e:
        print(e)
    finally:
        time.sleep(5)

if not is_deployed:
    send_discord_notification("서버 업데이트 실패")
    raise BaseException("nginx server is not reloaded successfully")

exec_cmd(f"docker compose -p {current_flag.lower()} down")
send_discord_notification("서버 업데이트 완료")
