export interface Message {
  id: string;
  content: string;
  role: USERS;
  created_at?: Date;
  hidden?: boolean;
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
  RESPONSE,
  OPTION,
  FORM,
  CITATION,
  TASK,
}

export interface Task {
  task_id: string;
  description: string;
  status: TaskStatus;
}

export interface TasksToComplete {
  // intent: string;
  // goal: string;
  // tasks: Task[];
  tasks: [];
  created_at?: Date;
}

export interface Response {
  response: string;
  tasks: [];
  form?: string;
  options: [];
  citation: string;
  text: string;
  agent_mode: string;
}

export type TextResponse = { created_at: Date; response: string; role?: USERS };

export type Options = { created_at: Date; options: string[]; role?: USERS };

export type Citation = { created_at: Date; citation: string; role?: USERS };

export type FormField = {
  label: string;
  type: string;
  placeholder: string;
  required: boolean;
};

export type DynamicFormData = {
  title: string;
  fields: FormField[];
};

export type Forms = { form: string; created_at: Date; role: USERS };
