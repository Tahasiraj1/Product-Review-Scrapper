import { Table, TableHeader, TableRow, TableHead, TableBody } from "./ui/table";

interface Review {
    product_name: string;
    review_text: string;
    rating: number;
    sentiment: string;
}


export default function ReviewTable({ reviews }: {  reviews: Review[] }) {
    return (
      <Table className="w-full border-collapse">
        <TableHeader>
          <TableRow className="bg-gray-200">
            <TableHead className="border p-2">Product Name</TableHead>
            <TableHead className="border p-2">Review Text</TableHead>
            <TableHead className="border p-2">Rating</TableHead>
            <TableHead className="border p-2">Sentiment</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {reviews.map((review, index) => (
            <TableRow key={index} className="even:bg-gray-100">
              <td className="border p-2">{review.product_name}</td>
              <td className="border p-2">{review.review_text}</td>
              <td className="border p-2">{review.rating}</td>
              <td className="border p-2">{review.sentiment}</td>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  }