"use client";
import React, { useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import TaskListContainer from "./TaskListContainer";

// The Task component to display each individual task
// const TaskItem = ({ task }: { task: Task }) => {
//   const getStatusLabel = () => {
//     switch (task.status) {
//       case TaskStatus.PENDING:
//         return "Pending";
//       case TaskStatus.IN_PROGRESS:
//         return "In Progress";
//       case TaskStatus.DONE:
//         return "Done";
//       default:
//         return "Unknown";
//     }
//   };

//   return (
//     <div className="task-item">
//       <div className="task-description">{task.description}</div>
//       <div className="task-status">{getStatusLabel()}</div>
//     </div>
//   );
// };

// Sidebar component to show tasks
const Sidebar = ({ tasksToComplete }: { tasksToComplete: string[] }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleSidebar = () => setIsExpanded((prev) => !prev);

  useEffect(() => {
    if (tasksToComplete && tasksToComplete.length > 0) {
      setIsExpanded(true);
    } else {
      setIsExpanded(false);
    }
  }, [tasksToComplete]);

  return (
    <div className="sidebar">
      <button onClick={toggleSidebar} className="sidebar-toggle-button">
        <ChevronLeft /> {/* Task button icon */}
      </button>
      {isExpanded && (
        <div className="task-list">
          <TaskListContainer tasks={tasksToComplete} intent={""} goal={""} />
          {/* {tasksToComplete.map((taskGroup) => (
            <div key={taskGroup.intent}>
              <h3>{taskGroup.intent}</h3>
              <div>
                {taskGroup.tasks.map((task: Task) => (
                  <TaskItem key={task.task_id} task={task} />
                ))}
              </div>
            </div>
          ))} */}
        </div>
      )}
    </div>
  );
};

export default Sidebar;
