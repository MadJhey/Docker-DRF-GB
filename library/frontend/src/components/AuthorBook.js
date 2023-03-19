import React from 'react'
import { useParams } from 'react-router-dom'
const BookItem = ({ item }) => {
    return (
        <tr>
            <td>{item.id}</td>
            <td>{item.name}</td>
            <td>{item.author.first_name}</td>
        </tr>
    )
}
const BookList = ({ items }) => {
    let { id } = useParams();
    let filtered_items = items.filter((item) => item.author.id == id)
    return (
        <table>
            <tr>
                <th>ID</th>
                <th>NAME</th>
                <th>AUTHOR</th>
            </tr>
            {filtered_items.map((item) => <BookItem item={item} />)}
        </table>
    )
}
export default BookList