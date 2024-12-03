// supabaseClient.js
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://hyvjlavtgxwqbogeguyt.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5dmpsYXZ0Z3h3cWJvZ2VndXl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNzcxMTYwNCwiZXhwIjoyMDQzMjg3NjA0fQ.3j55VcjneBr458XA5842kAWFhvzUSaMXvD8l5oTWhMc";

export const supabase = createClient(supabaseUrl, supabaseKey);
