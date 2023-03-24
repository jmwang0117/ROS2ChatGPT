FROM ros:humble

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y  ros-$ROS_DISTRO-filters  ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-joint-state-publisher \
                        ros-$ROS_DISTRO-robot-localization ros-$ROS_DISTRO-rtabmap-ros ros-$ROS_DISTRO-depth-image-proc \ 
                        ros-$ROS_DISTRO-navigation2 libuvc-dev tmux openssh-server openai
# install dependencies, some may fail but practically it's ok
RUN bash -c 'source /ros_entrypoint.sh && rosdep install --from-paths src -r -y || true'
WORKDIR /work/ros2_ws






