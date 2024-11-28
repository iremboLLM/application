import { languageModelAPI } from "@/api/language_model";
import { Query } from "@/lib/types";
import { useMutation } from "react-query";

export const useLanguageModelApi = () => {
  return useMutation({
    mutationFn: async (query: Query) => await languageModelAPI.generate(query),
  });
};
