// mongoose.d.ts
import mongoose from "mongoose";

declare global {
  // eslint-disable-next-line no-var
  var mongoose: {
    conn: mongoose.Connection | typeof import("mongoose") | null;
    promise: Promise<mongoose.Connection> | typeof import("mongoose") | null;
  };
}

// Prevent TypeScript from treating this file as a script
export {};
