import React from "react";

const TaskListHeader: React.FC<{ intent: string }> = ({ intent }) => {
  return (
    <div className="flex flex-col justify-between items-center gap-2">
      <div>
        <h1 className="text-xl font-medium text-center mb-5">{intent}</h1>
      </div>
      {/* <div className="inline-flex space-x-2 items-center justify-end">
        <a
          href="#"
          className="p-2 border border-slate-200 rounded-md inline-flex space-x-1 items-center text-indigo-200 hover:text-white bg-indigo-600 hover:bg-indigo-500"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-4 h-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span className="text-sm font-medium hidden md:block">Urgent</span>
        </a>
        <a
          href="#"
          className="p-2 border border-slate-200 rounded-md inline-flex space-x-1 items-center hover:bg-slate-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-4 h-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zM3.75 12h.007v.008H3.75V12zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm-.375 5.25h.007v.008H3.75v-.008zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
            />
          </svg>
          <span className="text-sm hidden md:block">Latest</span>
        </a>
      </div> */}
    </div>
  );
};

export default TaskListHeader;
