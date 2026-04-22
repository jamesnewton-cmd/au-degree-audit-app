export function Card({ className = "", children }) {
  return <div className={`ui-card ${className}`.trim()}>{children}</div>;
}

export function CardHeader({ className = "", children }) {
  return <div className={`ui-card-header ${className}`.trim()}>{children}</div>;
}

export function CardTitle({ className = "", children }) {
  return <h3 className={`ui-card-title ${className}`.trim()}>{children}</h3>;
}

export function CardContent({ className = "", children }) {
  return <div className={`ui-card-content ${className}`.trim()}>{children}</div>;
}
