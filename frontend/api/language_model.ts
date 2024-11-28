import { Query, Response } from "@/lib/types";
import axios from "axios";

class LanguageModelAPI {
  async generate(query: Query) {
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/agent`,
        query,
        {
          withCredentials: true,
        }
      );
      return response.data as Response;
    } catch (error) {
      console.error(error);
      throw new Error("An unexpected error occurred");
    }
  }
}

export const languageModelAPI = new LanguageModelAPI();
