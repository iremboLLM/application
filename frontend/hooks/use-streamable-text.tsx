import { useState, useEffect } from "react";

export const useStreamableText = (
  text: string,
  delay: number = 100
): string => {
  const [streamedText, setStreamedText] = useState<string>("");

  useEffect(() => {
    let index = 0;

    const intervalId = setInterval(() => {
      setStreamedText((prevText) => prevText + text[index]);
      index += 1;

      if (index === text.length) {
        clearInterval(intervalId); // Stop when the text is fully streamed
      }
    }, delay);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, [text, delay]);

  return streamedText;
};
