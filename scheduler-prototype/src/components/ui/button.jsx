import React from "react";

const STYLE_MAP = {
  default: "btn btn-default",
  outline: "btn btn-outline",
  secondary: "btn btn-secondary",
  destructive: "btn btn-destructive",
};

export function Button({ className = "", variant = "default", ...props }) {
  const style = STYLE_MAP[variant] || STYLE_MAP.default;
  return <button className={`${style} ${className}`.trim()} {...props} />;
}
