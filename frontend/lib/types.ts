export interface Message {
  id: string;
  content: string;
  role: USERS;
  created_at?: Date;
}

export interface Session {
  user: {
    id: string;
  };
}

export interface Query {
  query: string;
  agent_mode: string;
  thread_id: string;
}

export enum TaskStatus {
  PENDING,
  IN_PROGRESS,
  DONE,
}

export enum USERS {
  SYSTEM,
  USER,
  AI,
}

export interface Task {
  task_id: string;
  description: string;
  status: TaskStatus;
}

export interface TasksToComplete {
  intent: string;
  goal: string;
  tasks: Task[];
  created_at?: Date;
}

export interface Response {
  response: string;
  tasks_to_complete: TasksToComplete;
}
