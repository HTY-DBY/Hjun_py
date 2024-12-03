import subprocess


# %%

def check_conda_package(package_name, env_name=None):
	try:
		# 检查环境是否存在
		if env_name:
			env_check_command = ["conda", "env", "list"]
			result = subprocess.run(env_check_command, capture_output=True, text=True, check=True)
			envs = result.stdout

			# 如果环境不存在，抛出错误
			if env_name not in envs:
				raise ValueError(f"Environment '{env_name}' does not exist!")

		# 构造 `conda list` 命令
		command = ["conda", "list"]
		if env_name:
			command += ["-n", env_name]

		# 执行 `conda list` 命令
		result = subprocess.run(command, capture_output=True, text=True, check=True)
		installed_packages = result.stdout

		# 检查包名是否在已安装的包列表中
		if package_name in installed_packages:
			print(f"Package '{package_name}' is installed in environment '{env_name or 'base'}'.")
			return True
		else:
			print(f"Package '{package_name}' is NOT installed in environment '{env_name or 'base'}'.")
			return False
	except subprocess.CalledProcessError as e:
		raise RuntimeError(f"Failed to execute Conda command. Details: {e}")
	except FileNotFoundError:
		raise EnvironmentError("Conda is not installed or not in PATH.")


# 示例用法
package = "kraken2"
env = "hj"  # 替换为你的环境名称，或设置为 None 检查 base 环境

a = check_conda_package(package, env)
