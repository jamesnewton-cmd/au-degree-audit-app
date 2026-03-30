export function Badge({ children, variant = "default", className = "" }) {
  const cls =
    variant === "secondary"
      ? "badge badge-secondary"
      : variant === "destructive"
        ? "badge badge-destructive"
        : "badge";
  return <span className={`${cls} ${className}`.trim()}>{children}</span>;
}
