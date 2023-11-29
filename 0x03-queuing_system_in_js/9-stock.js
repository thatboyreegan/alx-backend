import { promisify } from 'util';
import { createClient } from 'redis';
import { express } from 'express';


const listProducts = [
    {
        id: 1,
        name: 'Suitcase 250',
        price: 100,
        stock: 4,
    },
    {
        id: 2,
        name: 'Suitcase 450',
        price: 100,
        stock: 10,
    },
    {
        id: 3,
        name: 'Suitcase 650',
        price: 350,
        stock: 2,
    },
    {
        id: 4,
        name: 'Suitcase 1050',
        price: 550,
        stock: 5,
    },
];

function getItemById(id) {
    for (let product of listProducts){
        if (product.id === id) {
            return product;
        };
    };
}

const client = createClient();

client.get = promisify(client.get)

function reserveStockById(itemId, stock) {
    client.set(`item.${itemId}`, stock)
}

async function getCurrentReservedStockById(itemId) {
    const stock = await client.get(`item.${itemId}`).then((value) => {
        if (!value) value = 0;
        return value;
    })
    return stock;
}
const app = express();
app.listen(1245);

app.get('/list_products', (req, res) => {
    const available_products = [];
    for (let product of listProducts) {
        available_products.push({
            itemid: product.id,
            itemName: product.name,
            price: product.price,
            initialAvailableQuantity: product.stock,
        });
    };

    res.json(available_products);
});

app.get('/list_products/:itemId', async (res, req) => {
    const { itemId } = req.params;
    const product = getItemById(itemId);
    if (!product) {
        res.json({ status: "Product not found" });
        return;
    }
    const currentQuantity = await getCurrentReservedStockById(itemId);

    res.json({
        itemId,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock,
        currentQuantity,
    });
})

app.get("/reserve_product/:itemId", async (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(itemId);
  
    if (!product) {
      res.json({ status: "Product not found" });
      return;
    };
    const currentQuantity = Number(await getCurrentReservedStockById(itemId));
    if (product.stock - currentQuantity <= 0) {
      res.json({ status: "Not enough stock available", itemId: 1 });
      return;
    };
  
    reserveStockById(itemId, currentQuantity + 1);
    res.json({ status: "Reservation confirmed", itemId: 1 });
});