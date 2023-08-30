export default function LabeledCheckbox({ label, value, setValue, id }) {
  return (
    <div>
      <input onChange={setValue} id={id} type="checkbox" checked={value} />
      <label htmlFor={id}>{label}</label>
    </div>
  );
}
