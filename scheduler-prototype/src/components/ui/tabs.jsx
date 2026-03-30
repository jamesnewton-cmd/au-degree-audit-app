import React, { createContext, useContext, useMemo, useState } from "react";

const TabsContext = createContext(null);

function Tabs({ defaultValue, children }) {
  const [value, setValue] = useState(defaultValue || "");
  const context = useMemo(() => ({ value, setValue }), [value]);
  return <TabsContext.Provider value={context}>{children}</TabsContext.Provider>;
}

function TabsList({ className = "", children }) {
  return <div className={`tabs-list ${className}`}>{children}</div>;
}

function TabsTrigger({ value, className = "", children }) {
  const ctx = useContext(TabsContext);
  const active = ctx?.value === value;
  return (
    <button
      type="button"
      className={`tabs-trigger ${active ? "is-active" : ""} ${className}`.trim()}
      onClick={() => ctx?.setValue(value)}
    >
      {children}
    </button>
  );
}

function TabsContent({ value, className = "", children }) {
  const ctx = useContext(TabsContext);
  if (ctx?.value !== value) return null;
  return <div className={className}>{children}</div>;
}

export { Tabs, TabsContent, TabsList, TabsTrigger };
