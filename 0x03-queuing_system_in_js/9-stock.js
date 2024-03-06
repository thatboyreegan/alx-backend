import { createClient } from 'redis';
import { promisify } from 'util';
import  express  from 'express';

const listProducts = [
    {
        id: 1,
        name: 'Suitcase 250',
        price: 50,
        stock: 4
    },
    {
        id: 2,
        name: 'Suitcase 450',
        price: 100,
        stock: 10
    },
    {
        id: 3,
        name: 'Suitcase 650',
        price: 350,
        stock: 2
    },
    {
        id: 4,
        name: 'Suitcase 1050',
        price: 550,
        stock: 5
    }
];

function getItemById(id) {
    for (let obj of listProducts ) {
        if (obj.id == id) {
            return obj;
        };
    }
}

const client = createClient();


client.GET = promisify(client.GET);

function reserveStockById(itemId, stock) {
    client.SET(`itemId.${itemId}`, stock);
};

async function getCurrentReservedStockById(itemId) {
    const stock = await client.GET(`itemId.${itemId}`).then((value) => {
        if (!value) value = 0;
        return value;
    });
    return stock;
};


const app = express();

app.get('/list_products', (req, res) => {
    const new_listProducts = [];
    for (let Obj of listProducts) {
        new_listProducts.push({
            itemId: Obj.id,
            itemName: Obj.name,
            price: Obj.price,
            initialAvailableQuantity: Obj.stock
        });
    };
    res.status(200).json(new_listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = req.params.itemId;

    const item = getItemById(itemId);

    if (item) {
        const value = await getCurrentReservedStockById(itemId);
        const return_value = {
            itemId,
            itemName: item.name,
            price: item.price,
            initialAvailableQuantity: item.stock,
            currentQuantity: value
        };
        res.status(200).json(return_value);
        return;
    } else {
        res.status(200).json({status: 'Product not found'});
        return;
    }
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = req.params.itemId;
    const item = getItemById(itemId);

    if (!item) {
        return res.status(200).json({status: 'Product not found'});
    }

    const currentQuantity = Number(await getCurrentReservedStockById(itemId));
    if(item.stock - currentQuantity <= 0) {
        return res.status(200).json({status: 'Not enough stock available', itemId})
    };

    reserveStockById(itemId, currentQuantity + 1);
    res.status(200).json({status: 'Reservation confirmed', itemId});
})

app.listen(1245);
