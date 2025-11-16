import docker
from flask import Blueprint, jsonify

docker_bp = Blueprint("docker_manager", __name__)
client = docker.from_env()

# ---------- List all containers ----------
@docker_bp.route("/docker/containers", methods=["GET"])
def list_containers():
    containers = client.containers.list(all=True)
    return jsonify([
        {
            "name": c.name,
            "id": c.short_id,
            "image": c.image.tags,
            "status": c.status,
        }
        for c in containers
    ])


# ---------- Container control ----------
@docker_bp.route("/docker/<string:name>/start", methods=["POST"])
def start_container(name):
    client.containers.get(name).start()
    return jsonify({"message": f"{name} started"})


@docker_bp.route("/docker/<string:name>/stop", methods=["POST"])
def stop_container(name):
    client.containers.get(name).stop()
    return jsonify({"message": f"{name} stopped"})


@docker_bp.route("/docker/<string:name>/restart", methods=["POST"])
def restart_container(name):
    client.containers.get(name).restart()
    return jsonify({"message": f"{name} restarted"})


# ---------- HEALTH & STATS ----------
@docker_bp.route("/docker/stats", methods=["GET"])
def container_stats():
    containers = client.containers.list(all=True)
    output = []

    for c in containers:
        try:
            stats = c.stats(stream=False)

            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            cpu_percent = (cpu_delta / system_delta * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100) if system_delta > 0 else 0

            mem_usage = stats["memory_stats"]["usage"]
            mem_limit = stats["memory_stats"].get("limit", 1)
            mem_percent = (mem_usage / mem_limit) * 100

            output.append({
                "name": c.name,
                "id": c.short_id,
                "status": c.status,
                "cpu": round(cpu_percent, 2),
                "memory": round(mem_percent, 2),
                "mem_raw": mem_usage,
                "mem_limit": mem_limit,
                "uptime": c.attrs["State"]["StartedAt"],
                "image": c.image.tags
            })
        except Exception as e:
            print("Stats Error:", e)
            continue

    return jsonify(output)


# ---------- Logs ----------
@docker_bp.route("/docker/<string:name>/logs", methods=["GET"])
def container_logs(name):
    container = client.containers.get(name)
    logs = container.logs(tail=200).decode()
    return jsonify({"logs": logs})
