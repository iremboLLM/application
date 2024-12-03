"use client";
import React, { useState } from "react";
import { DynamicFormData, USERS } from "@/lib/types";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useChatContext } from "@/context/Chat.context";

const DynamicForm: React.FC<{ formData: DynamicFormData }> = ({ formData }) => {
  const { addMessage, isLoading } = useChatContext();
  // Manage form state dynamically
  const [formValues, setFormValues] = useState(
    formData.fields.reduce((acc, field) => {
      acc[field.label] = ""; // Initialize each field's value to an empty string
      return acc;
    }, {} as Record<string, string>)
  );

  // Handle field changes
  const handleChange = (label: string, value: string) => {
    setFormValues((prev) => ({
      ...prev,
      [label]: value,
    }));
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Validate form if necessary (optional)
    const missingRequiredFields = formData.fields
      .filter((field) => field.required && !formValues[field.label])
      .map((field) => field.label);

    if (missingRequiredFields.length > 0) {
      alert(
        `Please fill in the required fields: ${missingRequiredFields.join(
          ", "
        )}`
      );
      return;
    }

    // Submit the form data (e.g., send to an API or process locally)
    console.log("Form submitted with values:", formValues);

    addMessage(USERS.USER, JSON.stringify(formValues), true);

    // Optional: Reset the form
    setFormValues(
      formData.fields.reduce((acc, field) => {
        acc[field.label] = ""; // Reset each field to an empty string
        return acc;
      }, {} as Record<string, string>)
    );
  };

  return (
    <div className="max-w-5xl p-8 border rounded-md shadow-md mt-5">
      <h1 className="text-2xl font-bold mb-5">{formData.title}</h1>
      <form className="space-y-4" onSubmit={handleSubmit}>
        {formData.fields.map((field, index) => (
          <div key={index} className="flex flex-col">
            <Label className="text-sm font-semibold mb-1">
              {field.label}
              {field.required && <span className="text-red-500">*</span>}
            </Label>
            {field.type === "textarea" ? (
              <Textarea
                className="p-2 border rounded-md"
                placeholder={field.placeholder}
                required={field.required}
                value={formValues[field.label]}
                onChange={(e) => handleChange(field.label, e.target.value)}
              />
            ) : (
              <Input
                type={field.type}
                className="p-2 border rounded-md"
                placeholder={field.placeholder}
                required={field.required}
                value={formValues[field.label]}
                onChange={(e) => handleChange(field.label, e.target.value)}
              />
            )}
          </div>
        ))}
        <Button
          disabled={isLoading}
          variant={"default"}
          type="submit"
          className="text-white py-2 px-4 rounded-md"
        >
          Submit
        </Button>
      </form>
    </div>
  );
};

export default DynamicForm;
