CREATE TABLE trunc_books AS SELECT
    customer_id,
    product_id,
    product_title,
    product_parent,
    star_rating,
    helpful_votes,
    review_headline,
    review_body,
    product_category,
    marketplace,
    review_date,
    verified_purchase
FROM books
WHERE customer_id IN (
                    SELECT customer_id
                    FROM books
                    GROUP BY customer_id
                    HAVING COUNT(star_rating)>=58
                    )
 AND product_id IN (
                    SELECT product_id
                    FROM books
                    GROUP BY product_id
                    HAVING COUNT(star_rating)>32
                    )
AND LENGTH(star_rating)<2;
