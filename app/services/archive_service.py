
from sqlalchemy.orm import Session
from app import crud, schemas

def archive_event_proposals(db: Session, event_id: int) -> int:
    """
    Archive all proposals submitted to an event when it closes.
    
    For each proposal (post) linked to the event with relation_type='submission':
    1. Create a clone of the post (type='archive', status='archived').
    2. Copy its content, title, and other metadata.
    3. Update the event-post relation to point to the new archived post.
    
    Returns:
        Number of proposals archived.
    """
    # 1. Get all submissions
    submissions = crud.event_posts.get_multi_by_category(
        db, event_id=event_id, relation_type="submission"
    )
    
    count = 0
    for rel in submissions:
        original_post = crud.posts.get(db, id=rel.post_id)
        if not original_post:
            continue
            
        # 2. Clone the post
        # We append "[Archived]" to title or similar distinction if needed, 
        # but usually just changing type/status is enough.
        archive_in = schemas.PostCreate(
            title=f"{original_post.title} (Snapshot)",
            content=original_post.content,
            type="archive", # Special type for archived snapshots
            visibility="public", # Keep public or match original
            # Copy other fields as needed
        )
        
        # Create the archive post
        # We set created_by to original author so they still own the credit, 
        # but they can't edit it because of status/logic checks elsewhere.
        archive_post = crud.posts.create(db, obj_in=archive_in)
        # Manually set status to 'archived' (if not settable via Create schema)
        archive_post.status = "archived"
        archive_post.created_by = original_post.created_by
        db.add(archive_post)
        db.flush() # Get ID
        
        # 3. Update the relation to point to the archive
        # We remove the old relation and create a new one, or update the existing one.
        # Updating is cleaner to preserve the 'created_at' of the submission if possible,
        # but relation ID might not matter. Let's update the post_id.
        rel.post_id = archive_post.id
        db.add(rel)
        
        # Optional: Link the archive back to original for traceability?
        # crud.post_posts.create(source=archive_post.id, target=original_post.id, type="snapshot_of")
        
        count += 1
        
    db.commit()
    return count
