import Tile from "../../common/tile";

export default function statistics() {
  return (
    <div>
      <Tile title="Total URLs" value={100} />
      <Tile title="Total clicks" value={200} />
      <Tile title="Active" value={50} />
    </div>
  );
}
