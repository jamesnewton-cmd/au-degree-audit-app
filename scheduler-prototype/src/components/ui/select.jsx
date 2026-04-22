import React from "react";

export function Select({ value, onValueChange, children }) {
  const options = React.Children.toArray(children).find(
    (child) => React.isValidElement(child) && child.type === SelectContent
  );
  return (
    <select
      value={value}
      onChange={(e) => onValueChange?.(e.target.value)}
      style={{
        width: "100%",
        marginTop: "0.5rem",
        borderRadius: "0.75rem",
        border: "1px solid #cbd5e1",
        padding: "0.62rem 0.75rem",
        background: "white",
        fontSize: "0.9rem",
      }}
    >
      {React.Children.map(options?.props?.children, (child) => {
        if (!React.isValidElement(child) || child.type !== SelectItem) return null;
        return (
          <option value={child.props.value} key={child.props.value}>
            {child.props.children}
          </option>
        );
      })}
    </select>
  );
}

export function SelectTrigger({ children }) {
  return <>{children}</>;
}

export function SelectValue() {
  return null;
}

export function SelectContent({ children }) {
  return <>{children}</>;
}

export function SelectItem({ children }) {
  return <>{children}</>;
}
