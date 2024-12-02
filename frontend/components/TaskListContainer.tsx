import React from "react";
import TaskListHeader from "./TaskListHeader";
import PaginatedTaskList from "./TaskItem";

interface TaskListContainerProps {
  tasks: string[];
  intent: string;
  goal: string;
}

const TaskListContainer: React.FC<TaskListContainerProps> = ({
  tasks,
  intent,
  goal,
}) => {
  return (
    <div className="max-w-5xl my-10 bg-white p-8 rounded-xl shadow shadow-slate-300">
      <TaskListHeader intent={intent} />
      <p className="text-slate-500">{goal}</p>
      <div id="tasks" className="my-5">
        <PaginatedTaskList tasks={tasks} />
      </div>
      <p className="text-xs text-slate-500 text-center">
        Last updated 1 minutes ago
      </p>
    </div>
  );
};

export default TaskListContainer;
