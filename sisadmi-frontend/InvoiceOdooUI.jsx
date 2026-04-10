import { useState } from "react";

const Card = ({ children }) => (
  <div style={{ border: "1px solid #ddd", borderRadius: "10px", padding: "15px", marginBottom: "10px" }}>
    {children}
  </div>
);

const Button = ({ children, ...props }) => (
  <button style={{ padding: "8px 12px", margin: "3px", cursor: "pointer" }} {...props}>
    {children}
  </button>
);

const Input = (props) => (
  <input style={{ padding: "6px", width: "100%" }} {...props} />
);

export default function InvoiceOdooUI() {
  const [lines, setLines] = useState([{ product: "", qty: 1, price: 0 }]);

  const updateLine = (index, field, value) => {
    const newLines = [...lines];
    newLines[index][field] = value;
    setLines(newLines);
  };

  const addLine = () => {
    setLines([...lines, { product: "", qty: 1, price: 0 }]);
  };

  const removeLine = (index) => {
    setLines(lines.filter((_, i) => i !== index));
  };

  const subtotal = lines.reduce((acc, l) => acc + l.qty * l.price, 0);
  const iva = subtotal * 0.12;
  const total = subtotal + iva;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 3fr", gap: "20px", padding: "20px" }}>
      
      {/* Sidebar */}
      <div>
        <Card>
          <Button onClick={saveInvoice}>Guardar</Button>
          <Button>Confirmar</Button>
          <Button>Cancelar</Button>
        </Card>
      </div>

      {/* Main */}
      <div>
        <Card>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
            <Input placeholder="Cliente" />
            <Input type="date" />
          </div>
        </Card>

        <Card>
          <table width="100%">
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio</th>
                <th>Subtotal</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {lines.map((line, index) => {
                const lineTotal = line.qty * line.price;
                return (
                  <tr key={index}>
                    <td>
                      <Input
                        value={line.product}
                        onChange={(e) => updateLine(index, "product", e.target.value)}
                      />
                    </td>
                    <td>
                      <Input
                        type="number"
                        value={line.qty}
                        onChange={(e) => updateLine(index, "qty", parseFloat(e.target.value))}
                      />
                    </td>
                    <td>
                      <Input
                        type="number"
                        value={line.price}
                        onChange={(e) => updateLine(index, "price", parseFloat(e.target.value))}
                      />
                    </td>
                    <td>{lineTotal.toFixed(2)}</td>
                    <td>
                      <Button onClick={() => removeLine(index)}>X</Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <Button onClick={addLine}>+ Agregar línea</Button>
        </Card>

        <Card>
          <div>Subtotal: {subtotal.toFixed(2)}</div>
          <div>IVA: {iva.toFixed(2)}</div>
          <div><strong>Total: {total.toFixed(2)}</strong></div>
        </Card>
      </div>
    </div>
  );
}

const saveInvoice = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/invoice/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        lines: lines
      })
    });

    const data = await response.json();

    alert("Factura guardada ID: " + data.invoice_id);

  } catch (error) {
    console.error(error);
    alert("Error al guardar");
  }
};